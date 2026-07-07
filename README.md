git remote set-url origin https://github.com/ТВОЙ_НИК/ReportFlow.git


git remote -v
origin	https://github.com/PetrZhelezin/Client.git (fetch)
origin	https://github.com/PetrZhelezin/Client.git (push)
PM> git remote set-url origin https://github.com/ТВОЙ_НИК/ReportFlow.git
PM> git remote set-url origin https://github.com/PetrZhelezin/ReportFlow.git
PM> git remote set-url origin https://github.com/G4sTt/ReportFlow
PM> git remote -v
origin	https://github.com/G4sTt/ReportFlow (fetch)
origin	https://github.com/G4sTt/ReportFlow (push)
PM> git push origin C#Part




git checkout pythonPart/python-api -- src


# Создать новый репозиторий в текущей папке
git init

# Клонировать существующий репозиторий
git clone https://github.com/username/repository.git

# Клонировать в конкретную папку
git clone https://github.com/username/repository.git /path/to/folder

# Клонировать конкретную ветку
git clone -b branch-name https://github.com/username/repository.git

# Проверить статус файлов (какие изменены, какие добавлены)
git status

# Добавить файл в индекс для следующего коммита
git add filename.txt

# Добавить все измененные файлы
git add .

# Добавить все файлы в конкретной папке
git add src/

# Зафиксировать изменения (сделать коммит)
git commit -m "Описание того, что было изменено"

# Закоммитить все измененные и отслеживаемые файлы (без git add)
git commit -am "Описание изменений"

# Посмотреть, к какому удаленному репозиторию подключен проект
git remote -v

# Добавить удаленный репозиторий
git remote add origin https://github.com/username/repository.git

# Изменить URL удаленного репозитория (если нужно переключиться на другой)
git remote set-url origin https://github.com/username/new-repository.git

# Удалить удаленный репозиторий
git remote remove origin

# Отправить изменения в удаленный репозиторий
git push origin main

# Отправить изменения в первый раз (создать связь с удаленной веткой)
git push -u origin branch-name

# Получить изменения из удаленного репозитория и слить с текущей веткой
git pull origin main

# Только получить информацию об изменениях (без слияния)
git fetch origin

# Получить все изменения из всех веток
git fetch --all

# Посмотреть все локальные ветки (текущая отмечена *)
git branch

# Посмотреть все ветки (локальные и удаленные)
git branch -a

# Создать новую ветку
git branch branch-name

# Создать ветку и сразу переключиться на нее
git checkout -b branch-name

# Переключиться на другую ветку
git checkout branch-name

# Переключиться на ветку из удаленного репозитория (создаст локальную копию)
git checkout origin/remote-branch-name

# Удалить локальную ветку
git branch -d branch-name

# Принудительно удалить ветку (даже если она не слита)
git branch -D branch-name

# Переименовать текущую ветку
git branch -m new-branch-name

# Отменить изменения в файле (вернуть к последнему коммиту)
git checkout -- filename.txt

# Отменить все изменения в рабочей директории
git checkout .

# Удалить файл из Git (но оставить на диске)
git rm --cached filename.txt

# Удалить файл из Git и с диска
git rm filename.txt

# Удалить папку рекурсивно
git rm -r folder-name

# Отменить последний коммит, но оставить изменения в файлах
git reset --soft HEAD~1

# Отменить последний коммит и убрать изменения из индекса (файлы останутся измененными)
git reset HEAD~1

# Полностью отменить последний коммит (ВСЕ изменения пропадут!)
git reset --hard HEAD~1

# Отменить коммит, создав новый "обратный" коммит (безопасно для публичных репо)
git revert commit-hash


