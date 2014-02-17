from flask import request


def create_token(**kwargs):
    pass


def refresh_token(**kwargs):
    pass


def oauth():
    args = request.args.to_dict()

    if args['grant_type'] == 'password':
        create_token(**args)
    elif args['grant_type'] == 'refresh_token':
        refresh_token(**args)

    return '* token here *'