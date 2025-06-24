# Development Guide

## Project Structure

```
fintech-llm-finetuning/
├── data/                    # Data storage
│   ├── raw/                # Raw downloaded data
│   │   └── wealth_data/    # Financial data
│   └── finetuned_models/   # Finetuned model checkpoints
├── src/                    # Source code
│   ├── data_collection/    # Data collection scripts
│   ├── preprocessing/      # Data preprocessing scripts
│   ├── training/          # Model training scripts
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── config/                # Configuration files
└── docs/                 # Documentation
```

## Development Workflow

1. **Code Organization**
   - Keep utility functions in `src/utils/`
   - Use consistent naming conventions
   - Document all functions and classes

2. **Testing**
   - Write tests for new functionality
   - Run tests before committing: `pytest tests/`
   - Maintain test coverage

3. **Data Management**
   - Store raw data in `data/raw/`
   - Process data in `src/preprocessing/`
   - Save processed data in appropriate formats

4. **Model Training**
   - Configuration in `config/`
   - Training scripts in `src/training/`
   - Save models in `data/finetuned_models/`

5. **Documentation**
   - Update docs when adding features
   - Include usage examples
   - Document API changes

## Best Practices

1. **Code Style**
   - Use Black for formatting
   - Follow PEP 8 guidelines
   - Write clear docstrings

2. **Version Control**
   - Write clear commit messages
   - Create feature branches
   - Review code before merging

3. **Error Handling**
   - Use proper exception handling
   - Log errors appropriately
   - Include error messages

4. **Performance**
   - Use rate limiting for APIs
   - Implement proper caching
   - Monitor memory usage

## Common Tasks

### Adding New Data Source
1. Create script in `src/data_collection/`
2. Use utility functions from `src/utils/`
3. Add tests in `tests/`
4. Update documentation

### Training New Model
1. Update config in `config/`
2. Use training script in `src/training/`
3. Save model in `data/finetuned_models/`
4. Document model details

### Adding New Feature
1. Create feature branch
2. Add tests
3. Update documentation
4. Submit pull request 