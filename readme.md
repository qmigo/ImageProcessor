**Image Processor** 

Follow these steps to setup the project

1. Import project from Github
```
git clone https://github.com/qmigo/ImageProcessor.git ImageProcessor
cd ImageProcessor
```

2. Create a virtual env and activate
```
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Setup .env configuration
Here you can use local MySQL database connection parameters but you need a cloudinary account (refer assets/Image Processor LLD:appendix)

5. Run the application
```
python app:app
```

6. Test application by using this postman collection
```
https://documenter.getpostman.com/view/15331466/2sAYdioVbM
```

To access all documentation navigate to /assets
