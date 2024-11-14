```markdown
# HyenaDNA Training Pipeline

A pipeline for training HyenaDNA models on genomic sequences using AWS SageMaker and HealthOmics.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure AWS credentials and region

3. Open the notebook in SageMaker Studio:
   - Navigate to notebooks/train_hyena_dna.ipynb
   - Follow the instructions in the notebook

## Project Structure
- `notebooks/`: Contains the main training notebook
- `scripts/`: Helper modules for AWS sessions, data handling, and training
  - `session_handler.py`: AWS/SageMaker session management
  - `data_handler.py`: HealthOmics data access
  - `training_handler.py`: Training configuration and execution

## Usage
See `notebooks/train_hyena_dna.ipynb` for detailed usage instructions.
```