З декоратором `@api.model` можна використовувати різні методи, які впливають на поведінку моделі та можуть бути викликані без прив'язки до конкретного запису. Ось декілька з них:

1. `create(self, vals)`: Метод викликається при створенні нового запису в моделі. Він дозволяє вам змінити або доповнити дані, перед тим як вони будуть збережені.

2. `search(self, args, offset=0, limit=None, order=None)`: Метод викликається для пошуку записів у моделі. Він дозволяє вам виконати пошук з використанням певних умов та отримати результати з заданим обмеженням.

3. `read(self, fields=None, load='_classic_read')`: Метод дозволяє читати дані з записів у моделі. Ви можете вказати, які поля вам потрібно отримати, та використовувати різні механізми для зчитування даних.

4. `write(self, vals)`: Метод викликається для збереження змін у записі моделі. Він дозволяє вам змінити значення полів та зберегти зміни.

5. `unlink(self)`: Метод викликається для видалення запису з моделі. Він дозволяє вам видалити запис, якщо це дозволено у моделі.

6. `default_get(self, fields)`: Метод дозволяє отримати значення за замовчуванням для нового запису перед створенням.

7. `onchange(self, values, field_name, field_onchange)`: Метод дозволяє виконати дії при зміні значень полів у записі.

8. `copy(self, default=None)`: Метод дозволяє здійснити копіювання запису у моделі.

9. `name_search(self, name, args=None, operator='ilike', limit=100)`: Метод дозволяє виконати пошук за ім'ям (назвою) у записах моделі.

10. `browse(self, ids, prefetch=None)`: Метод дозволяє переглядати записи за їхніми ідентифікаторами.

Ці методи дозволяють вам здійснювати різні дії з моделлю та даними, що в ній зберігаються, без прив'язки до конкретного запису. Вони надають вам більшу гнучкість та контроль над поведінкою вашої моделі.