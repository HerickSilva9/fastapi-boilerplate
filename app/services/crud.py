from sqlalchemy.orm import Session


def create(db: Session, instance: object):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance