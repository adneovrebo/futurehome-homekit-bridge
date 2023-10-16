import os, dotenv

dotenv.load_dotenv()

app_name = "fhtohomekit"
futurehome_ip = os.getenv("FUTUREHOME_IP")
username = os.getenv("FUTUREHOME_USERNAME")
password = os.getenv("FUTUREHOME_PASSWORD")
uid="9bb1be75-35d7-4069-ac00-b974315f7ec3"