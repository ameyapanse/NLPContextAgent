import os


def set_keys():
    with open('keys/openai_api_key') as f:
        os.environ['OPENAI_API_KEY'] = f.read()
    with open('keys/huggingfacehub_api_token') as f:
        os.environ['HUGGINGFACEHUB_API_TOKEN'] = f.read()


if __name__ == "__main__":
    set_keys()
    print(os.environ['OPENAI_API_KEY'])
    print(os.environ['HUGGINGFACEHUB_API_TOKEN'])
