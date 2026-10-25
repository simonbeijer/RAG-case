from app.config import load_config


def main() -> None:
    """Function to run CLI and test prompts"""
    print(load_config())
    
if __name__ == "__main__":
    
    main()