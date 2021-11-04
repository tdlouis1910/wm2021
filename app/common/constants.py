RESPONSE = {
    'SUCCESS': {
        'result': 'SUCCESS',
        'status': 200
    },
    'VALIDATION_ERROR': {
        'result': 'VALIDATION_ERROR',
        'status': 400
    },
    'UNAUTHENTICATED': {
        'result': 'UNAUTHENTICATED',
        'needLogin': True,
        'status': 401
    },
    'WRONG_TOKEN': {
        'result': 'WRONG_TOKEN',
        'needLogin': True,
        'status': 401
    },
    'UNAUTHORIZED': {
        'result': 'UNAUTHORIZED',
        'status': 403
    },
    'NOT_FOUND': {
        'result': 'NOT_FOUND',
        'status': 404
    },
    'SERVER_ERROR': {
        'result': 'SERVER_ERROR',
        'status': 500
    }
}