def main():
    with open("main0.html", "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open("1.txt", "w", encoding="utf-8") as f_w:
        for line in lines:
            if "ac-name-text" in line:
                f_w.write(line)
            if "price-btn-text" in line:
                f_w.write(line)


if __name__ == '__main__':
    main()
