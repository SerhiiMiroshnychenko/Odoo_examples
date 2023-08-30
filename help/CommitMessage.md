__Tag and module name__

Tags are used to prefix your commit. They should be one of the following

`IN ODOO DOCS`

`[FIX]` for bug fixes: mostly used in stable version but also valid if you are fixing a recent bug in development version;
        _для виправлення помилок: переважно використовується у стабільній версії, але також дійсний, якщо ви виправляєте нещодавню помилку у версії для розробки;_

`[REF]` for refactoring: when a feature is heavily rewritten;
        _для рефакторингу: коли функція сильно переписана;_

`[ADD]` for adding new modules;
        _для додавання нових модулів;_

`[REM]` for removing resources: removing dead code, removing views, removing modules, …;
        _для видалення ресурсів: видалення мертвого коду, видалення переглядів, видалення модулів, …;_

`[REV]` for reverting commits: if a commit causes issues or is not wanted reverting it is done using this tag;
        _для повернення комітів: якщо коміт спричиняє проблеми або небажаний, скасування виконується за допомогою цього тегу;_

`[MOV]` for moving files: use git move and do not change content of moved file otherwise Git may loose track and history of the file; also used when moving code from one file to another;
        _для переміщення файлів: використовуйте git move і не змінюйте вміст переміщеного файлу, інакше Git може втратити відстеження та історію файлу; також використовується при переміщенні коду з одного файлу в інший;_ 

`[REL]` for release commits: new major or minor stable versions;
        _для комітів випуску: нові основні або другорядні стабільні версії;_

`[IMP]` for improvements: most of the changes done in development version are incremental improvements not related to another tag;
        _для покращень: більшість змін, зроблених у версії розробки, є поступовими вдосконаленнями, не пов’язаними з іншим тегом;_

`[MERGE]` for merge commits: used in forward port of bug fixes but also as main commit for feature involving several separated commits;
          _для комітів злиття: використовується в переданому порті виправлень помилок, але також як основний комміт для функції, що включає кілька окремих комітів;_

`[CLA]` for signing the Odoo Individual Contributor License;
        _за підписання Ліцензії окремого учасника Odoo;_

`[I18N]` for changes in translation files;
         _за зміни файлів перекладу;_

`IN STS`

[ERP] [DEV] __Розробка на git__
Існує мінімум 2 гілки `master` і `dev` 

`master` - основний код, який працює на продакшині клієнта
`dev` - тут відбувається все тестування

Мердж гілки dev в будь-яку іншу гілку категорично заборонено

Логіка:
1. Для кожного таску робимо нову гілку з номером таску (credea-erp-0001, task-9464 ...) і в ній робимо всю розробку. Нову гілку робимо тільки від master
2. Опис коментаря для коміта __#branch: [DEV, FIX, REF] descriptoin ( task-9464: [DEV] Added new fields)__
3. Після закінчення розробки гілку master мерджимо в гілку нашого таску, після цього мерджимо нашу гілку в dev
4. Тестуємо
5. Якщо тестування пройшло добре, без помилок, робимо кодревью
6. Якщо тестування пройшло добре, без помилок, гілку master мерджимо в гілку нашого таску а потім нашу гілку мерджимо в  гілку master
7. Якщо під час тестування виникли помилки, то всі виправлення робимо в гілці таску, і після цього робимо пункти 2, 3, 4, 5
8. Мердж гілки dev в будь-яку іншу гілку категорично заборонено

Якщо виникне ситуація, коли розробка ведеться на декілька версій Одоо, тоді список гілок виглядатиме так:
12.0
13.0
dev_12.0
dev_13.0

Ваші гілки
dev_12.0_task#
dev_13.0_task#

EXIGO, EVACARE
Існує 3 гілки: `master`, `stage`, `dev` 

`master` - основний код, який працює на продакшині клієнта
`stage` - тут відбувається тестування коду перед злиттям гілки з master
`dev` - тут відбувається все тестування

Логіка:
1. Для кожного таску робимо нову гілку з номером таску (credea-erp-0001, task-9464 ...) і в ній робимо всю розробку. Нову гілку робимо тільки від master
2. Опис коментаря для коміта номер таску назва таску: опис (__PMT-324 Global bug: Added new fields__)
3. Після закінчення розробки гілку master мерджимо в гілку нашого таску, після цього мерджимо нашу гілку в dev
4. Тестуємо
5. Якщо тестування пройшло добре, без помилок, робимо кодревью
6. Якщо тестування пройшло добре, без помилок, повторно гілку stage мерджимо в гілку нашого таску а потім нашу гілку мерджимо в гілку stage
7. Якщо під час тестування виникли помилки, то всі виправлення робимо в гліці таску, і після цього робимо пункти 2, 3, 4, 5
8. Проводимо повторне тестування але вже гілки stage
9. Тільки гілка stage мерждиться в master
