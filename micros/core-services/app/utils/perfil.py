
class ProfileUtils:
    @staticmethod
    def format_profile_name(name: str) -> str:
        """Formatea el nombre del perfil eliminando espacios extra y poniendo en mayúsculas la primera letra de cada palabra."""
        return name.strip().title()
