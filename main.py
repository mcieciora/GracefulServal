from website import create_app


def app():
    return create_app()


if __name__ == '__main__':
    app().run(debug=True)
