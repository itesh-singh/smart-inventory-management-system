from alerts.models import Alert


def sync_stock_alerts(stock_item):
    product = stock_item.product

    Alert.objects.filter(
        product=product,
        is_resolved=False
    ).update(is_resolved=True)

    if stock_item.quantity_on_hand == 0:
        Alert.objects.create(
            alert_type=Alert.OUT_OF_STOCK,
            product=product,
            message=f"{product.name} is out of stock.",
            is_resolved=False,
        )

    elif stock_item.quantity_on_hand <= stock_item.reorder_level:
        Alert.objects.create(
            alert_type=Alert.LOW_STOCK,
            product=product,
            message=f"{product.name} is running low.",
            is_resolved=False,
        )