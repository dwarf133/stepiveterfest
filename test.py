from conrtollers import qr_controller
if __name__ == "__main__":
    # qr_controller.proceed_order(334884)
    print(qr_controller.Order.get_order(334884))