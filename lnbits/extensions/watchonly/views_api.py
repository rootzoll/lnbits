import hashlib
from flask import g, jsonify, request, url_for
from http import HTTPStatus

from lnbits.core.crud import get_user
from lnbits.decorators import api_check_wallet_key, api_validate_post_request
from lnbits.settings import FORCE_HTTPS

from lnbits.extensions.watchonly import watchonly_ext
from .crud import (
    create_watch_wallet,
    get_watch_wallet,
    get_watch_wallets,
    update_watch_wallet,
    delete_watch_wallet,
    create_payment,
    get_payment,
    get_payments,
    delete_payment,
)



###################WALLETS#############################

@watchonly_ext.route("/api/v1/wallet", methods=["GET"])
@api_check_wallet_key("invoice")
def api_wallets_retrieve():

    try:
        return (
            jsonify(get_watch_wallets(g.wallet.user)),
            HTTPStatus.OK,
        )
    except:
        return (
            jsonify({"message": "Cant fetch."}),
            HTTPStatus.UPGRADE_REQUIRED,
        )

@watchonly_ext.route("/api/v1/wallet/<wallet_id>", methods=["GET"])
@api_check_wallet_key("invoice")
def api_wallet_retrieve(wallet_id):
    wallet = get_watch_wallet(wallet_id) 
        
    if not wallet:
        return jsonify({"message": "wallet does not exist"}), HTTPStatus.NOT_FOUND

    return jsonify({wallet}), HTTPStatus.OK


@watchonly_ext.route("/api/v1/wallet", methods=["POST"])
@watchonly_ext.route("/api/v1/wallet/<wallet_id>", methods=["PUT"])
@api_check_wallet_key("invoice")
@api_validate_post_request(
    schema={
        "ex_key": {"type": "string", "empty": False, "required": True},
        "description": {"type": "string", "empty": False, "required": True},
        "amount": {"type": "integer", "min": 1, "required": True},
    }
)
def api_wallet_create_or_update(wallet_id=None):

    if not wallet_id:
        wallet = create_watch_wallet(g.wallet.user, g.data.ex_key, g.data.description, g.data.amount)
        return jsonify(get_watch_wallet(wallet)), HTTPStatus.CREATED

    else:
        wallet = update_watch_wallet(wallet_id, g.data) 
        return jsonify({wallet}), HTTPStatus.OK 


@watchonly_ext.route("/api/v1/wallet/<wallet_id>", methods=["DELETE"])
@api_check_wallet_key("invoice")
def api_wallet_delete(wallet_id):
    wallet = get_watch_wallet(wallet_id)

    if not wallet:
        return jsonify({"message": "Wallet link does not exist."}), HTTPStatus.NOT_FOUND

    delete_watch_wallet(wallet_id)

    return "", HTTPStatus.NO_CONTENT



#############################PAYEMENTS##########################

@watchonly_ext.route("/api/v1/payment", methods=["GET"])
@api_check_wallet_key("invoice")
def api_payments_retrieve():

    try:
        return (
            jsonify(get_payments(g.wallet.user)),
            HTTPStatus.OK,
        )
    except:
        return (
            jsonify({"message": "Cant fetch."}),
            HTTPStatus.UPGRADE_REQUIRED,
        )

@watchonly_ext.route("/api/v1/payment/<payment_id>", methods=["GET"])
@api_check_wallet_key("invoice")
def api_payment_retrieve(payment_id):
    payment = get_payment(payment_id) 
        
    if not payment:
        return jsonify({"message": "payment does not exist"}), HTTPStatus.NOT_FOUND

    return jsonify({payment}), HTTPStatus.OK


@watchonly_ext.route("/api/v1/payment", methods=["POST"])
@watchonly_ext.route("/api/v1/payment/<payment_id>", methods=["PUT"])
@api_check_wallet_key("invoice")
@api_validate_post_request(
    schema={
        "ex_key": {"type": "string", "empty": False, "required": True},
        "pub_key": {"type": "string", "empty": False, "required": True},
        "amount": {"type": "integer", "min": 1, "required": True},
    }
)
def api_payment_create_or_update(payment_id=None):

    if not payment_id:
        payment = create_payment(g.wallet.user, g.data.ex_key, g.data.pub_key, g.data.amount)
        return jsonify(get_payment(payment)), HTTPStatus.CREATED

    else:
        payment = update_payment(payment_id, g.data) 
        return jsonify({payment}), HTTPStatus.OK 


@watchonly_ext.route("/api/v1/payment/<payment_id>", methods=["DELETE"])
@api_check_wallet_key("invoice")
def api_payment_delete(payment_id):
    payment = get_watch_wallet(payment_id)

    if not payment:
        return jsonify({"message": "Wallet link does not exist."}), HTTPStatus.NOT_FOUND

    delete_watch_wallet(payment_id)

    return "", HTTPStatus.NO_CONTENT
