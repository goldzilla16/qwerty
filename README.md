# CI/CD Capstone Project: Task Management API

> **Student:** [Your Name]  
> **Project:** Automated CI/CD Pipeline with Testing & Code Quality  
> **Academic Year:** 2024-2025

---

## 📋 Project Overview

This capstone project implements a **complete CI/CD pipeline** that automates unit testing and code quality analysis for a Flask REST API. The pipeline ensures code reliability through automated testing and maintains code quality standards using SonarQube.

---

## 🎯 Project Objectives

1. ✅ **Automate Testing** - Unit tests run on every push
2. ✅ **Maintain Code Quality** - SonarQube quality gates enforce standards
3. ✅ **Generate Metrics** - Coverage reports and quality dashboards
4. ✅ **Fail Fast** - Stop pipeline if tests or quality checks fail
5. ✅ **Professional Workflow** - Industry-standard practices

---

## 🛠️ Technology Stack

- **Framework:** Flask 3.0.0
- **Testing:** Pytest 7.4.3 with pytest-cov
- **Code Quality:** SonarQube Cloud
- **CI/CD:** GitHub Actions
- **Language:** Python 3.9
- **Database:** SQLite (in-memory for tests)

---

## 📁 Project Structure

```
cicd-capstone/
├── .github/
│   └── workflows/
│       └── main.yml              # CI/CD pipeline
│
├── app/
│   ├── __init__.py               # Package initialization
│   └── app.py                    # Flask application
│
├── tests/
│   ├── __init__.py
│   └── test_app.py               # Comprehensive unit tests
│
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
├── requirements.txt              # Dependencies
├── sonar-project.properties      # SonarQube config
└── pytest.ini                    # Pytest configuration
```

---

## 🚀 Task Management API

A Flask REST API with endpoints for CRUD operations on tasks.

### Features
- ✅ Create, read, update, delete tasks
- ✅ Task status tracking
- ✅ Health check endpoint
- ✅ Comprehensive error handling
- ✅ RESTful design

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/api/tasks` | List all tasks |
| GET | `/api/tasks/<id>` | Get specific task |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/<id>` | Update task |
| DELETE | `/api/tasks/<id>` | Delete task |

---

## 🧪 Testing

### Test Coverage
- **17 comprehensive tests** covering all endpoints
- **Edge cases and error scenarios**
- **>85% code coverage** (SonarQube quality gate)

### Run Tests Locally

```bash
# Run all tests
pytest -v

# Run with coverage report
pytest --cov=app --cov-report=term --cov-report=xml -v

# Run specific test
pytest tests/test_app.py::test_get_all_tasks -v
```

---

## 🔄 CI/CD Pipeline

### Pipeline Stages

```
Developer Push
    ↓
GitHub Actions Triggers
    ↓
Stage 1: Unit Testing (pytest)
    ├─ ✅ Pass → Continue to Stage 2
    └─ ❌ Fail → STOP (Quality Gate 1)
    ↓
Stage 2: Code Quality (SonarQube)
    ├─ ✅ Pass → Pipeline Success
    └─ ❌ Fail → STOP (Quality Gate 2)
    ↓
Pipeline Complete
```

### Quality Gates

**Pytest Gate:**
- All tests must pass
- Coverage must be >80%
- No test failures allowed

**SonarQube Gate:**
- No critical/blocker issues
- Code coverage >80%
- No security vulnerabilities
- Code smells and duplications checked

---

## 🔐 GitHub Secrets Required

```
SONAR_TOKEN           # SonarQube authentication token
SONAR_HOST_URL        # https://sonarcloud.io
```

---

## 📊 SonarQube Dashboard

Your project dashboard shows:
- 📈 Code coverage percentage
- 🐛 Bugs and vulnerabilities
- 💨 Code smells
- 📏 Complexity metrics
- ⭐ Maintainability rating

Access at: `https://sonarcloud.io/dashboard?id=YOUR_PROJECT_KEY`

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.9+
- Git
- GitHub account
- SonarCloud account

### Local Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/cicd-capstone.git
cd cicd-capstone

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -v

# Run application
python -m app.app
```

Visit `http://localhost:5000`

---

## 🔧 Configuration

### SonarQube Setup

1. **Go to [SonarCloud.io](https://sonarcloud.io)**
2. **Sign in with GitHub**
3. **Create organization** (or use existing)
4. **Analyze new project**
5. **Select your repository**
6. **Choose "With GitHub Actions"**
7. **Get your project key and organization**

### Update sonar-project.properties

```properties
sonar.projectKey=YOUR_PROJECT_KEY
sonar.organization=YOUR_ORG_KEY
```

### GitHub Secrets

1. **Settings** → **Secrets and variables** → **Actions**
2. **Add SONAR_TOKEN**
3. **Add SONAR_HOST_URL** (https://sonarcloud.io)

---

## 📈 Success Metrics

✅ **All tests pass locally**
✅ **Coverage report generated**
✅ **Pipeline triggers on push**
✅ **Pytest stage passes**
✅ **SonarQube quality gate passes**
✅ **Dashboard shows metrics**
✅ **Pipeline stops on failure**

---

## 🐛 Troubleshooting

### Tests Failing?
```bash
# Run locally first
pytest -v

# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Coverage not showing in SonarQube?
- Verify `coverage.xml` is generated
- Check `sonar-project.properties` path
- Ensure `SONAR_TOKEN` is correct

### Quality gate failing?
- Check SonarQube dashboard for specific issues
- Fix code smells or security issues
- Re-run tests

---

## 📚 Learning Outcomes

- ✅ CI/CD pipeline design
- ✅ Automated testing with pytest
- ✅ Code quality analysis
- ✅ GitHub Actions workflow
- ✅ Quality gates and metrics
- ✅ Professional development practices

---

## 📄 References

1. Flask Documentation - https://flask.palletsprojects.com/
2. Pytest Documentation - https://docs.pytest.org/
3. GitHub Actions - https://docs.github.com/en/actions
4. SonarQube Cloud - https://sonarcloud.io/

---

**Project Status:** ✅ Complete  
**Last Updated:** 2024