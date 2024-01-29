def main(running_as_script=False):
    print("hello world")
    if running_as_script:
        print("running as script")
    else:
        print("not running as script")
    return


if __name__ == "__main__":
    main(running_as_script=True)
