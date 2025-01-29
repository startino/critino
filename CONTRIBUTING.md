# Contributing to Critino

We welcome developer contributions! This guide focuses on the **API** setup.

- 🚧 **Frontend (SvelteKit) & Database (Supabase)**: Contribution guides coming soon! Currently you can contribute to the API independently from the database and frontend.

---

## 🛠️ API Development

### Prerequisites

- **Python 3.11–3.12**
- **Docker** and **Docker Compose**
- [Nixpacks](https://nixpacks.com):

  ```bash
  curl -sSL https://nixpacks.com/install.sh | bash
  ```

- [Poetry](https://python-poetry.org) (Python dependency management):

  ```bash
  pip install poetry
  ```

### First-Time Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/startino/critino
   ```

2. Install Python dependencies:

   ```bash
   cd services/api && poetry install
   ```

3. Build and start the API (from the repo root):

   ```bash
   ./api.sh  # First time only – build api containers with Nixpacks and starts Docker services
   ```

### Running the API (from the repo root)

```bash
docker compose up api  # Use this for daily development
```

### Workflow

- **Format code**:

  ```bash
  ./services/api/scripts/format.sh
  ```

- **Lint code**:

  ```bash
  ./services/api/scripts/lint.sh    # (existing errors are expected)
  ```

---

## 🤝 Contribution Process

1. Fork the repository and create a feature/bugfix branch.
2. Ensure your code passes formatting/linting checks.
3. Open a PR with:
   - A clear description of changes
   - Links to relevant issues (if applicable)

---

## 🚧 Testing & Quality

- _Tests_: We’re working on a testing framework – contributions welcome!
- _Linting_: Fix **new** lint errors only; legacy cleanup is tracked separately.

---

## 🔮 Future Areas

- **Pre-commit hooks**: Help us automate checks!
- **Frontend/Database guides**: WIP for SvelteKit/Supabase contributions.

---

🙌 Thank you for supporting Critino’s mission to improve AI feedback systems!
