import copy

def shimbel_otterman(matrix_a):
    n = len(matrix_a)
    inf = float('inf')
    
    A_1 = copy.deepcopy(matrix_a)
    Paths = [[ [] for _ in range(n)] for _ in range(n)]
    
    print("\n=== Матрица A^1 и Q^1 (0 промежуточных вершин) ===\n")
    print_matrices("A^1", A_1, "Q^1", Paths, target_len=0)
    
    A_current = copy.deepcopy(A_1)
    Paths_current = copy.deepcopy(Paths)
    
    for step in range(2, n):
        A_next = [[inf] * n for _ in range(n)]
        Paths_next = [[ [] for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                min_val = inf
                best_path = []
                
                # Умножение Шимбелла - Оттермана
                for m in range(n):
                    val = A_current[i][m] + A_1[m][j]
                    if val < min_val:
                        min_val = val
                        if m == i:
                            best_path = []
                        elif m == j:
                            best_path = Paths_current[i][j]
                        else:
                            best_path = Paths_current[i][m] + [m + 1]
                
                A_next[i][j] = min_val
                if min_val != inf:
                    Paths_next[i][j] = best_path
                else:
                    Paths_next[i][j] = []
                    
        print(f"=== Матрица A^{step} и Q^{step} (ТОЛЬКО {step-1} промежуточные вершины) ===\n")
        print_matrices(f"A^{step}", A_next, f"Q^{step}", Paths_next, target_len=step-1)
        
        A_current = copy.deepcopy(A_next)
        Paths_current = copy.deepcopy(Paths_next)

def print_beautiful_matrix(name, matrix_data):
    n = len(matrix_data)
    if n == 0: return
    
    col_widths = [max(len(matrix_data[r][c]) for r in range(n)) for c in range(n)]
    
    prefix = f"{name} = "
    empty_prefix = " " * len(prefix)
    mid_idx = n // 2
    
    for i, row in enumerate(matrix_data):
        formatted_row = "  ".join(row[c].rjust(col_widths[c]) for c in range(n))
        
        if n == 1:
            left, right = "( ", " )"
        elif i == 0:
            left, right = "⎛ ", " ⎞"
        elif i == n - 1:
            left, right = "⎝ ", " ⎠"
        else:
            left, right = "⎜ ", " ⎟"
        
        current_prefix = prefix if i == mid_idx else empty_prefix
        print(f"{current_prefix}{left}{formatted_row}{right}")
    print()

def print_matrices(name_a, A, name_q, Paths, target_len):
    n = len(A)
    
    str_A = []
    for row in A:
        # Для целых чисел отбрасываем .0, чтобы вывод был красивее
        str_A.append([str(int(x)) if x != float('inf') and x == int(x) else str(x) if x != float('inf') else '∞' for x in row])
        
    str_Q = []
    for row in Paths:
        row_str = []
        for p in row:
            if len(p) == target_len and target_len > 0:
                row_str.append(",".join(map(str, p)))
            else:
                row_str.append("0")
        str_Q.append(row_str)
        
    print_beautiful_matrix(name_a, str_A)
    print_beautiful_matrix(name_q, str_Q)
    print("-" * 50 + "\n")

def input_matrix():
    print("=== Метод Шимбелла — Оттермана ===")
    while True:
        try:
            n = int(input("Введите размерность матрицы (количество вершин): "))
            if n <= 0:
                print("Число должно быть положительным.")
                continue
            break
        except ValueError:
            print("Пожалуйста, введите целое число.")
            
    print(f"\nВведите матрицу {n}x{n} по строкам.")
    print("Разделяйте числа пробелами. Если пути нет, пишите 0 или inf.")
    print("(Нули вне главной диагонали автоматически заменятся на ∞)\n")
    
    matrix = []
    for i in range(n):
        while True:
            row_str = input(f"Строка {i+1}: ").strip().split()
            if len(row_str) != n:
                print(f"Ошибка: ожидалось {n} элементов, получено {len(row_str)}. Повторите ввод.")
                continue
            
            row = []
            valid = True
            for j, val in enumerate(row_str):
                if val.lower() in ['inf', '∞']:
                    row.append(float('inf'))
                else:
                    try:
                        num = float(val) if '.' in val else int(val)
                        # Автоматическая замена нулей на бесконечность (если это не диагональ)
                        if i != j and num == 0:
                            row.append(float('inf'))
                        else:
                            row.append(num)
                    except ValueError:
                        print(f"Ошибка: '{val}' не является числом. Повторите ввод строки.")
                        valid = False
                        break
            if valid:
                matrix.append(row)
                break
    return matrix

if __name__ == "__main__":
    try:
        user_matrix = input_matrix()
        shimbel_otterman(user_matrix)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
