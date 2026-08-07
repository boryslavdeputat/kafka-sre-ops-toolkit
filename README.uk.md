# Kafka SRE Ops Toolkit

**Мови:** [English](README.md) · [Українська](README.uk.md)

> Практичний матеріал від [Boryslav Deputat](https://github.com/boryslavdeputat) - Cloud / SRE / Platform.
> Сайти: [Portfolio](https://boryslavdeputat.com/) · [ClawDBot / KLAV (UA AI)](https://clawdbot.llc/) · [Walk ATX Pet](https://walkatxpet.com/) · [DepuTater](https://deputater.com/)

Python-інструменти для **Apache Kafka / Amazon MSK**: lag, under-replicated partitions, rebalance, capacity, incident runbooks.

## Можливості

| Інструмент | Призначення |
|------------|-------------|
| `kafka_lag_snapshot.py` | Знімок lag consumer group |
| `under_replicated.py` | URP |
| `topic_capacity.py` | Оцінка capacity |
| Runbooks у `docs/` | Інциденти та rebalance |

## Швидкий старт

```bash
pip install -r requirements.txt
python scripts/kafka_lag_snapshot.py --bootstrap $BOOTSTRAP --group my-group --format table
```

## Відмова від відповідальності

Освітній і практичний матеріал. Перевіряйте під ваші compliance, cost і SLO перед production.

## Контакти

- Portfolio: https://boryslavdeputat.com/
- ClawDBot / KLAV (UA AI): https://clawdbot.llc/
- Email: info@boryslavdeputat.com

## Ліцензія

MIT - див. [LICENSE](LICENSE).
