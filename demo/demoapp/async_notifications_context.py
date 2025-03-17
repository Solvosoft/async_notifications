def import_context():
    context = [
        ("fieldname", "Field description"),
        ("fieldname2", "Field description"),
    ]
    return {
        "code": "yourcode",
        "subject": "your subject",
        "context": context,
        "message": None,
        "as_template": False,
    }


def import_multiple_context():
    context = [
        ("fieldname", "Field description"),
        ("fieldname2", "Field description"),
    ]
    return (
        {
            "code": "yourcode_one",
            "subject": "your subject A",
            "context": context,
            "message": None,
            "as_template": False,
        },
        {
            "code": "yourcode_two",
            "subject": "your subject B",
            "context": context,
            "message": None,
            "as_template": False,
        },
    )
