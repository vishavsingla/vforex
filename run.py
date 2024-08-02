import logging
from app import create_app

if __name__ == '__main__':
    logging.basicConfig(filename='logs/app.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    app = create_app()
    app.run(debug=True)
