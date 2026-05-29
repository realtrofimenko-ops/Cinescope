import pytest

from db_requester.models import AccountTransactionTemplate
def test_accounts_transaction_template_negative(db_session):

    # Создаем тестовые аккаунты
    stan = AccountTransactionTemplate(
        user="Stan_test",
        balance=100
    )

    bob = AccountTransactionTemplate(
        user="Bob_test",
        balance=500
    )

    db_session.add_all([stan, bob])
    db_session.commit()

    # Проверяем начальные значения
    assert stan.balance == 100
    assert bob.balance == 500

    try:

        # Пытаемся перевести больше чем есть
        if stan.balance < 200:
            raise ValueError("Недостаточно средств")

        stan.balance -= 200
        bob.balance += 200

        db_session.commit()

    except Exception:

        # Откат транзакции
        db_session.rollback()

    # Обновляем данные из БД
    db_session.refresh(stan)
    db_session.refresh(bob)

    # Проверяем что ничего не изменилось
    assert stan.balance == 100
    assert bob.balance == 500

    # Cleanup
    db_session.delete(stan)
    db_session.delete(bob)
    db_session.commit()