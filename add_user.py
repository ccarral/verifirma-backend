from getpass import getpass
import termcolor
import database as db


def main():
    prompt = " >> "
    print("Proceso de alta de un nuevo usuario")
    print("-----------------------------------\n")
    print("Ingrese el número de cuenta del usuario:")
    num_cuenta = input(prompt)

    print("Ingrese el (los) nombre(s) del usuario:")
    nombres = input(prompt)

    print("Ingrese el primer apellido del usuario:")
    primer_apellido = input(prompt)

    print("Ingrese el segundo apellido del usuario:")
    segundo_apellido = input(prompt)

    while True:
        print("Ingrese la contraseña del usuario:")
        pass1 = getpass(prompt)
        print("Confirme la contraseña: ")
        pass2 = getpass(prompt)
        if pass1 != pass2:
            print("Las contraseñas no coinciden, inténtelo de nuevo")
            continue

        break

    print("Ingrese la etiqueta con la que se identificará al usuario:")
    etiqueta = input(prompt)

    datos = {
        "num_cuenta": num_cuenta,
        "nombres": nombres,
        "primer_apellido": primer_apellido,
        "segundo_apellido": segundo_apellido,
        "password_hash": db.sha256_base64(pass1),
        "etiqueta": etiqueta
    }

    db.insert_user(datos)


if __name__ == "__main__":
    main()
