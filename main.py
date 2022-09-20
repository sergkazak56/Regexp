import csv
import re

# Функция поиска и замены телефоноф в соответсвии с регулярными выражениями:
def sub_phones(contacts_list):
    """
    Функция поиска и замены телефоноф в соответсвии с регулярными выражениями
    :param contacts_list: входящий список
    :return: contacts_list: исходящий список с отформатированными телефонами
    """
    pattern = r"(\+7|8)\s*?\(?(495)\)?[-\s*]?(\d{3})[-\s*]?(\d{2})[-\s*]?(\d{2})\s?\(?[доб\.]*\s?(\d*)\)?"
    sub_with_add = r"+7(\2)\3-\4-\5 доб.\6"
    sub_without_add = r"+7(\2)\3-\4-\5"
    for person in contacts_list[1:]:
        phone = person[5]
        if phone:
            if re.search(pattern, phone).group(6):
                person[5] = re.sub(pattern, sub_with_add, phone)
            else:
                person[5] = re.sub(pattern, sub_without_add, phone)
    return contacts_list

# Функция слияния двух списков:
def list_combine(list1, list2):
    """
    Функция слияния двух списков. В случае если в одном списке элемент - пустая строка,
    а во втором соотвествующий элемент присутствует, то в new_list будет занесен элемент
    из второго списка и наоборот. В случае пустой строки в обеих списках в new_list также
    будет занесена пустая строка.
    :param list1: cписок1
    :param list2: список2
    :return: new_list - возвращаемый список
    """
    new_list = []
    for item in range(len(list1)):
        if list1[item] and list2[item]:
            new_list.append(list1[item])
        elif list1[item] and not list2[item]:
            new_list.append(list1[item])
        elif not list1[item] and list2[item]:
            new_list.append(list2[item])
        else:
            new_list.append('')
    return new_list

# Функция сравнения двух списков:
def list_comparison(list1, list2):
    """
    Списки считаются равными, если первые два элемента обоих списков соотвественно равны
    :param list1: cписок1
    :param list2: список2
    :return: False: если списки не равны.
             list_combine(list1, list2): если списки равны
    """
    if list1[0] == list2[0] and list1[1] == list2[1]:
        return list_combine(list1, list2)
    else:
        return False

# Функция упорядочивания имен, отчеств и фамилий в списках
def sub_persons_names(contacts_list):
    """
    Функция упорядочивания имен, отчеств и фамилий в списках с помощью регулярного выражения,
    а также удаления дублирующих строк
    :param contacts_list: входящий список
    :return: contacts_list: исходящий упорядоченный список
    """
    pattern = r"([А-ЯЁ][а-яё]+)\s?([А-ЯЁ]*[а-яё]*)\s?([А-ЯЁ]*[а-яё]*)"
    for person in contacts_list[1:]:
        if person[0] and re.search(pattern, person[0]).group(3):
            person[1] = re.search(pattern, person[0]).group(2)
            person[2] = re.search(pattern, person[0]).group(3)
            person[0] = re.search(pattern, person[0]).group(1)
        elif person[0] and re.search(pattern, person[0]).group(2):
            if not person[1]:
                person[1] = re.search(pattern, person[0]).group(2)
                person[0] = re.search(pattern, person[0]).group(1)
            elif not person[2]:
                person[2] = re.search(pattern, person[0]).group(2)
                person[0] = re.search(pattern, person[0]).group(1)
        elif person[1] and re.search(pattern, person[1]).group(2):
            person[2] = re.search(pattern, person[1]).group(2)
            person[1] = re.search(pattern, person[1]).group(1)
    for item1 in range(1, len(contacts_list)):
        for item2 in range(item1+1, len(contacts_list)):
            if list_comparison(contacts_list[item1], contacts_list[item2]):
                contacts_list[item1] = list_comparison(contacts_list[item1], contacts_list[item2])
                contacts_list.pop(item2)
                break
    return contacts_list

# Функция считывания csv файла, манипуляций с данными и записи нового csv файла
def main():
    """
    Функция считывает файл "phonebook_raw.csv", упорядочивает записи в полученном списке и
    записывает новый файл "phonebook.csv" в текущий каталог
    """
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows_csv = csv.reader(f, delimiter=",")
        contacts_list = list(rows_csv)
    new_contacts_list = sub_phones(contacts_list)
    new_contacts_list = sub_persons_names(new_contacts_list)
    csv.register_dialect("writecsv", delimiter=",", quoting=csv.QUOTE_NONE, escapechar="\\", lineterminator='\n')
    with open("phonebook.csv", "w", encoding='utf-8') as f:
      datawriter = csv.writer(f, "writecsv")
      datawriter.writerows(new_contacts_list)


if __name__ == '__main__':
    main()
