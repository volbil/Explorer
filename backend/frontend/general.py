from webargs.flaskparser import use_args
from ..services import BlockService
from flask import redirect, url_for
from flask import render_template
from .args import search_args
from pony import orm

def init(blueprint):
    @blueprint.route("/search")
    @use_args(search_args, location="query")
    @orm.db_session
    def search(args):
        if args["query"].isdigit():
            if (block := BlockService.get_by_height(args["query"])):
                return redirect(url_for("frontend.block", blockhash=block.blockhash))

        else:
            if len(args["query"]) == 64:
                if (block := BlockService.get_by_hash(args["query"])):
                    return redirect(url_for("frontend.block", blockhash=block.blockhash))

                return redirect(url_for("frontend.transaction", txid=args["query"]))

            else:
                return redirect(url_for("frontend.address", address=args["query"]))

        return redirect(url_for("frontend.home"))

    @blueprint.route("/docs")
    def docs():
        return render_template("layout.html")
