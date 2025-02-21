from uuid import uuid4 as uuid
from ..mysql import Database


def save_login(user: str, ip: str):
    with Database() as db:
        try:
            query = """
                    INSERT INTO audit_usuarios
                    (auus_ip, auus_descripcion, auus_action,  auus_usuario)
                    VALUES(%s, %s, NULL, %s);
                """

            db.execute(query, (ip, "Login", user))
        except Exception as e:
            print(e)
            return None


def save_audit_user(
    db, ip, actions: list, user: str, description: str, target_user: str
):
    try:
        with Database() as db:
            toSave = []
            for action in actions:
                if len(action) < 4:
                    raise ValueError("Each action must have at least 4 elements.")

                toSave.append(
                    {
                        "name": action[0],
                        "name_bd": action[1],
                        "value": action[2],
                        "show": action[3],
                    }
                )
            id = str(uuid())
            query = """
                INSERT INTO audit_user
                (auus_id, auus_ip, auus_description, auus_action,  auus_user)
                VALUES(%s, %s, %s, %s,  %s);
            """

            db.execute(
                query, (id, ip, description, str(toSave), user, target_user)
            )
    except Exception as e:
        print(e)
        return None
