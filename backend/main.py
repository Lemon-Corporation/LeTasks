from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped, mapped_column
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import jwt
from jose import JWTError
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:////app/data/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
user_project = Table('user_project', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('project_id', Integer, ForeignKey('projects.id'))
)

class Achievement(Base):
    __tablename__ = "achievements"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="achievements")

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    projects: Mapped[List["Project"]] = relationship("Project", secondary=user_project, back_populates="users")
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="assignee")
    achievements: Mapped[List["Achievement"]] = relationship("Achievement", back_populates="user")
    rank: Mapped[Optional[str]] = mapped_column(default="Employee")
    is_active: Mapped[bool] = mapped_column(default=True)
    avatar: Mapped[Optional[str]]

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    users: Mapped[List[User]] = relationship("User", secondary=user_project, back_populates="projects")
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[Optional[str]]
    status: Mapped[str]
    priority: Mapped[str]
    due_date: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    project: Mapped[Project] = relationship("Project", back_populates="tasks")
    assignee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    assignee: Mapped[Optional[User]] = relationship("User", back_populates="tasks")

Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    password: Optional[str] = None

class UserProfile(BaseModel):
    username: str
    email: str
    avatar: Optional[str] = None
    rank: Optional[str] = None

    class Config:
        orm_mode = True

class UserStats(BaseModel):
    totalTasks: int
    completedTasks: int
    ongoingTasks: int
    overdueTasks: int

class ProjectCreate(BaseModel):
    name: str

class ProjectOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_superuser: bool

    class Config:
        orm_mode = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    due_date: str
    project_id: int
    assignee: Optional[str] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: str
    completed: bool
    project: ProjectOut
    assignee: Optional[UserOut]

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    completed: Optional[bool] = None
    project_id: Optional[int] = None
    assignee: Optional[str] = None

    class Config:
        orm_mode = True

class AssignProjectRequest(BaseModel):
    user_id: int
    project_id: int

class AchievementOut(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True

# Security
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user

def get_user_stats(db: Session, user_id: int):
    total_tasks = db.query(Task).filter(Task.assignee_id == user_id).count()
    completed_tasks = db.query(Task).filter(Task.assignee_id == user_id, Task.status == "Done").count()
    ongoing_tasks = db.query(Task).filter(Task.assignee_id == user_id, Task.status != "Done").count()
    overdue_tasks = db.query(Task).filter(
        Task.assignee_id == user_id,
        Task.status != "Done",
        Task.due_date < datetime.now().strftime("%Y-%m-%d")
    ).count()

    return UserStats(
        totalTasks=total_tasks,
        completedTasks=completed_tasks,
        ongoingTasks=ongoing_tasks,
        overdueTasks=overdue_tasks
    )

def get_user_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.assignee_id == user_id).all()

def get_user_achievements(db: Session, user_id: int):
    return db.query(Achievement).filter(Achievement.user_id == user_id).all()

def update_user_rank(db: Session, user_id: int, new_rank: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.rank = new_rank
        db.commit()
        return True
    return False

def add_user_achievement(db: Session, user_id: int, achievement_title: str, achievement_description: str):
    new_achievement = Achievement(title=achievement_title, description=achievement_description, user_id=user_id)
    db.add(new_achievement)
    db.commit()
    return new_achievement

# FastAPI app
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Adjust this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.post("/api/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/users/", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/users/me", response_model=UserProfile)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/api/users/me/stats", response_model=UserStats)
async def read_user_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_stats(db, current_user.id)

@app.get("/api/users/me/tasks", response_model=List[TaskOut])
async def read_user_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_tasks(db, current_user.id)

@app.get("/api/users/me/achievements", response_model=List[AchievementOut])
async def read_user_achievements(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_achievements(db, current_user.id)

@app.put("/api/users/me", response_model=UserProfile)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        current_user.email = user_update.email
    if user_update.avatar:
        current_user.avatar = user_update.avatar
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@app.post("/api/projects/", response_model=ProjectOut)
async def create_project(project: ProjectCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_project = Project(name=project.name)
    db_project.users.append(current_user)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/api/projects/", response_model=List[ProjectOut])
async def read_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.is_superuser:
        return db.query(Project).all()
    else:
        return current_user.projects

@app.post("/api/tasks/", response_model=TaskOut)
async def create_task(
    task: TaskCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    print(f"Received task data: {task}")  # Add this line for debugging
    project = db.query(Project).filter(Project.id == task.project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if current_user not in project.users and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="User not authorized for this project")
    
    assignee = None
    if task.assignee:
        assignee = db.query(User).filter(User.username == task.assignee).first()
        if not assignee:
            raise HTTPException(status_code=404, detail=f"User {task.assignee} not found")

    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id,
        assignee_id=assignee.id if assignee else None
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/api/tasks/", response_model=List[TaskOut])
async def read_tasks(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if current_user.is_superuser:
        return db.query(Task).all()
    
    user_tasks = (
        db.query(Task)
        .filter(
            (Task.assignee_id == current_user.id) |
            (Task.project_id.in_([project.id for project in current_user.projects]))
        )
        .all()
    )
    
    return user_tasks

@app.put("/api/tasks/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Received task data: {task}")  # Добавьте логирование
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user not in db_task.project.users and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    update_data = task.dict(exclude_unset=True)

    if 'assignee' in update_data:
        assignee = db.query(User).filter(User.username == update_data['assignee']).first()
        if not assignee:
            raise HTTPException(status_code=404, detail=f"User {update_data['assignee']} not found")
        update_data['assignee_id'] = assignee.id
        del update_data['assignee']

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted successfully"}

@app.get("/api/projects/{project_id}/users", response_model=List[UserOut])
async def get_project_users(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not current_user.is_superuser and current_user not in project.users:
        raise HTTPException(status_code=403, detail="Not authorized to view this project's users")
    
    return project.users

# Superuser dashboard routes
@app.get("/api/admin/users", response_model=List[UserOut])
async def read_all_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(User).all()

@app.post("/api/admin/assign-project")
async def assign_project_to_user(
    request: AssignProjectRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == request.user_id).first()
    project = db.query(Project).filter(Project.id == request.project_id).first()
    
    if not user or not project:
        raise HTTPException(status_code=404, detail="User or Project not found")
    
    if project not in user.projects:
        user.projects.append(project)
        db.commit()
    return {"detail": "Project assigned successfully"}

@app.post("/api/admin/remove-user-from-project")
async def remove_user_from_project(
    request: AssignProjectRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = db.query(User).filter(User.id == request.user_id).first()
    project = db.query(Project).filter(Project.id == request.project_id).first()
    
    if not user or not project:
        raise HTTPException(status_code=404, detail="User or Project not found")
    
    if project in user.projects:
        user.projects.remove(project)
        db.commit()
    return {"detail": "User removed from project successfully"}

@app.post("/api/admin/create-task-for-user")
async def create_task_for_user(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")

    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    assignee = None
    if task.assignee:
        assignee = db.query(User).filter(User.username == task.assignee).first()
        if not assignee:
            raise HTTPException(status_code=404, detail=f"User {task.assignee} not found")

    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id,
        assignee_id=assignee.id if assignee else None
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/api/admin/users/{user_id}/rank")
async def update_rank(
    user_id: int,
    rank: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    success = update_user_rank(db, user_id, rank)
    if success:
        return {"message": "Rank updated successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/admin/users/{user_id}/achievements")
async def add_achievement(
    user_id: int,
    title: str,
    description: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    new_achievement = add_user_achievement(db, user_id, title, description)
    return {"message": "Achievement added successfully", "achievement": new_achievement}

# Initialization
def init_db():
    db = SessionLocal()
    try:
        # Create superuser if not exists
        superuser = db.query(User).filter(User.is_superuser == True).first()
        if not superuser:
            superuser = User(
                username="ArtShocheck",
                email="artshocheck@vk.com",
                hashed_password=get_password_hash("1234567890KEKAhaha"),
                is_superuser=True,
                rank="Employee",
                is_active=True
            )
            db.add(superuser)
            db.commit()
            db.refresh(superuser)

        # Create initial projects
        initial_projects = ["LemonID", "Lemma", "TracsAI", "Worlds", "Mayont", "LemOS", "Sontrum", "Artefact", "SafeThisSpace", "Citrus"]
        for project_name in initial_projects:
            project = db.query(Project).filter(Project.name == project_name).first()
            if not project:
                project = Project(name=project_name)
                db.add(project)
                superuser.projects.append(project)
        
        db.commit()
    finally:
        db.close()

# Run initialization
init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)