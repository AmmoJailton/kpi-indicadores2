    def get_info(self):
        now = datetime.datetime.now()
        return {
            "statusCode": 201,
            "version": __version__,
            "env": os.getenv("ENV"),
            "Status": f"A requisição foi feita em: {now}",
        }