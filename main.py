import json
import os


def load_civgraph(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def generate_makefile(graph, output_file="Makefile", task_dir="completed_tasks"):
    # Проверим, существует ли директория для завершённых задач
    if not os.path.exists(task_dir):
        os.makedirs(task_dir)

    with open(output_file, 'w') as makefile:
        makefile.write(f"TASK_DIR = {task_dir}\n\n")

        # Добавим цель по умолчанию (например, завершение всех задач)
        makefile.write("all: " + " ".join(graph.keys()) + "\n\n")

        # Генерируем цель для каждой задачи
        for task, dependencies in graph.items():
            task_file = os.path.join(task_dir, task)

            # Записываем цель с проверкой на существование файла
            makefile.write(f"{task}: {' '.join(dependencies)} | $(TASK_DIR)\n")
            makefile.write(f"\t@if not exist {task_file} (\n")
            makefile.write(f"\t\techo Выполняется задача: {task}\n")
            makefile.write(f"\t\ttype nul > {task_file}\n")  # Аналог touch на Windows
            makefile.write("\t)\n\n")

        # Цель для создания директории с завершёнными задачами
        makefile.write(f"$(TASK_DIR):\n")
        makefile.write(f"\t@mkdir $(TASK_DIR)\n\n")

        # Добавляем цель clean
        makefile.write(f"clean:\n")
        makefile.write(f"\t@del /Q /F $(TASK_DIR)\\*\n")
        makefile.write(f"\t@rmdir /Q $(TASK_DIR)\n")


if __name__ == "__main__":
    # Загрузка civgraph.json и генерация Makefile
    civgraph = load_civgraph("civgraph.json")
    generate_makefile(civgraph)
