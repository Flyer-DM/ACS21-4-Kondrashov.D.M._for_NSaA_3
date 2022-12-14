Использование параллельного программирования

1. Написать программу, перемножающую две матрицы поэлементно. Элементы матрицы-произведения должны вычисляться в несколько потоков.

Функция, вызываемая для расчёта элемента матрицы (она вызывается в отдельном потоке):
![image](https://user-images.githubusercontent.com/113033685/199028318-bae46eb8-5d75-42af-826a-005fd7466b7a.png)

Функция, возвращающая новую матрицу (результат умножения двух):
![image](https://user-images.githubusercontent.com/113033685/199028361-d4af60cc-caa9-4c66-8691-3c0e65323480.png)

3. Используйте пул процессов, чтобы распределять вычисления между определенным заранее количеством процессов, не зависящим от размеров матрицы.

В функции multiply используется Pool процессов, который определяет заранее количество процессов на основании количества столбцов в первой матрицы и строк во второй. По итогу вычисления получается список чисел - элементов новой матрицы, который преобразуется в матрицу размерности lines на columns с помощью функции list_reshaper:
![image](https://user-images.githubusercontent.com/113033685/199028635-9027174d-d852-4277-95c0-cdfbce278ab5.png)

4. Модифицируйте программу, чтобы элементы результирующей матрицы записывались в промежуточный файл сразу по факту их вычисления.

В функцию multiply можно задать необязательный параметр path - путь к файлу сохранения, тогда с использованием механизма очереди модуля multiprocessing элементы матрицы будут вычисляться и походу выполнения вычислений сразу же записываться в указанный файл path с помощью функции write_elem:
![image](https://user-images.githubusercontent.com/113033685/199028728-05328bb7-d57f-41d3-b88a-34ea97d515ac.png)

2. Программа должна читать две матрицы из исходных файлов. Матрица-произведение также должна записываться в файл.

Функция чтения матрицы из файла:

![image](https://user-images.githubusercontent.com/113033685/199028845-6085c454-202f-46b1-ba7a-662fa00492d7.png)

Функция сохранения матрицы в указанный файл:
![image](https://user-images.githubusercontent.com/113033685/199028883-b7abcdef-0929-4ce9-9c34-dff0f5618afa.png)

Дополнительно сделан декоратор для обработки ошибок при взаимодействии с файловой системой:
![image](https://user-images.githubusercontent.com/113033685/199028978-b186cece-f007-4a72-b4e3-d648a787223f.png)


Пример работы программы:
![image](https://user-images.githubusercontent.com/113033685/199029028-bd503d2b-f436-473a-8ba1-e75ea0ad922a.png)

Файлы:

![image](https://user-images.githubusercontent.com/113033685/199029077-a1a1bf88-5afe-4195-8946-03cc88bfb2f5.png)

![image](https://user-images.githubusercontent.com/113033685/199029094-5a840f73-1b73-425c-9396-3955a3c907af.png)

![image](https://user-images.githubusercontent.com/113033685/199029101-76fc0056-c857-4097-a955-832c79035170.png)
