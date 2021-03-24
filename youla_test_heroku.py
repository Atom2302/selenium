from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

        # В цикде While скролим страницу до конца,-
        # - собираем ссылки на карточки авто и -
        # - кликаем на элемент следующей страницы (Если следующая страница есть)
def write_url_car(page_number, page_count,no_page, driver):
    y = 1

    # Скролим
    while page_number <= page_count:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(10)
        print('**' * 30,'\n')

        # Получаем ссылки на авто и записываем в файл
        data_info = driver.find_elements_by_css_selector(
            "a[class='SerpSnippet_name__3F7Yu SerpSnippet_titleText__1Ex8A blackLink']")
        if data_info == []:
            print('NO')
        for i in data_info:
            print(f"{y}: {i.get_attribute('innerHTML').title()}:\n{i.get_attribute('href')}")
            print('==' * 30)
            with open('data/url_car.txt', 'a') as f:
                f.write(str(i.get_attribute('href') + '\n'))
            y += 1

        # Кликаем на следующую страничку (если имеется)
        if no_page == 0:
            try:
                driver.implicitly_wait(10)
                click_page = driver.find_element_by_css_selector(
                    "div[class='Paginator_block__2XAPy app_roundedBlockWithShadow__1rh6w']"+
                    f" a[data-page='{page_number+1}']")
                click_page.click()
                print('click')
                driver.implicitly_wait(10)
                driver.forward()
            except Exception as e:
                print('Страниц больше нет...')
        page_number += 1


def youla_category_and_url_car():
    url = 'https://auto.youla.ru/moskva'
    url_page = 'https://auto.youla.ru/moskva/cars/used/?bodyTypes%5B0%5D='
    # driver = webdriver.Firefox(executable_path='assets/geckodriver')
    # ~ driver = webdriver.Chrome(executable_path='assets/chromedriver')

    driver = webdriver.PhantomJS(executable_path='assets/phantomjs')

    # Переходим в раздел категорий автомобилей и берем блок с категориями
    driver.get(url)
    div_bloc = driver.find_element_by_css_selector("div\
        [class='BodyTypesRotator_itemsWrapper__2Lcre']")
    div_bloc = div_bloc.find_elements_by_css_selector(
                "div[class='BodyTypesRotator_item__27Jl6']")

    # Задаем переменные цикла
    number_category = []
    page_count = True
    page_number = 1
    no_page = 0

    # Получаем id категорий авто
    for i in div_bloc:
        number_category.append(i.get_attribute('data-id'))

    # Итерируем список категорий подставляя в URL адрес
#---(итерирую срез с 7-ой категории, так как в предыдущих слишком много машин,оч долго ждать.) 
    for i in number_category:
        driver.get(url_page + i) # Переходим в  категорию
        # scroll_down = driver.find_element_by_tag_name('html')

        # Получаем количество страниц категории
        try:
            page_count = driver.find_element_by_css_selector(
            "div[class='Paginator_total__oFW1n']")
        except Exception as e:
            no_page = 1
            print('Всего одна страница\n')
            page_count = 1
            # Вызываем функцию получаем url карточек в файл
            write_url_car(page_number, page_count,no_page, driver)
        else:
            page_count = int(page_count.get_attribute('innerText').split(' ')[1])
            print(f'Всего страниц: {page_count}\n')
            # Вызываем функцию получаем url карточек в файл
            write_url_car(page_number, page_count,no_page, driver) 
    driver.quit()

def main():
    youla_category_and_url_car()


if __name__ == "__main__":
    main()
