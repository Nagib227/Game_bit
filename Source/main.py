from Start_window import start_window
from Main_f import main


if __name__ == "__main__":
    pl = main(btn=start_window())
    while True:
        if pl == "kill":
            main(btn=start_window())
        if type(pl[0]) == int and type(pl[1]) == list:
            main(exp=pl[0], hp=pl[1])
