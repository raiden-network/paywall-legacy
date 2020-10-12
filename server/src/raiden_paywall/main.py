import glob
import os
from dataclasses import dataclass
import dataclasses
import datetime
from typing import Optional
import hashlib

import markdown2
from flask_cors import CORS
from flask import Flask, abort, jsonify, current_app

from raiden_paywall.flask_raiden import RaidenPaywall


@dataclass
class Endpoint:
    id: str
    content: str
    preview: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    preview: Optional[str] = None
    date: datetime.date = None
    image_url: Optional[str] = None

    @property
    def preview_dict(self):
        article_dict = dataclasses.asdict(self)
        preview_dict = {k:v for k,v in article_dict.items() if k in 
                        ('id', 'preview', 'title', 'description', 'date', 'image_url')}
        return preview_dict


    @classmethod
    def generate_from_markdown(cls, markdown_path):
        html = markdown2.markdown_path(markdown_path, extras=["metadata", "target-blank-links"])
        date = html.metadata.get('date')
        if date:
            try:
                date = datetime.datetime.date(date)
            except TypeError:
                pass
        return cls(
            id=hashlib.md5(html.encode('utf-8')).hexdigest(),
            content=html,
            preview=html.metadata.get('preview'),
            title=html.metadata.get('title'),
            description=html.metadata.get('description'),
            date=date,
            image_url=html.metadata.get('imageUrl'),
        )



def get_markdown_assets(search_path):
    """
    This assumes a flat folder structure for now (no recursive searching).
    """
    os.chdir(search_path)
    return glob.glob('./*.md')


# For now, use global dict
ENDPOINTS = {}  # UUID -> Endpoint
BASE_PRICE = 0.0000001


app = Flask(__name__)
CORS(app)
paywall = RaidenPaywall(app)


@app.before_first_request
def generate_endpoints():
    global ENDPOINTS

    path = current_app.config.get('ASSETS_PATH')
    if not path:
        return

    for path in get_markdown_assets(path):
        endpoint = Endpoint.generate_from_markdown(path)
        ENDPOINTS[endpoint.id] = endpoint


@app.route('/')
def overview():
    overview = []
    for id_, endpoint in ENDPOINTS.items():
        preview = endpoint.preview_dict
        assert id_ == endpoint.id
        preview['path'] = f'/articles/{id_}'
        overview.append(preview)
    return jsonify(overview)


@app.route('/articles/<uuid>')
def raiden_pulse(uuid):
    article = ENDPOINTS.get(uuid)
    if not article:
        abort(404)

    paywall.amount += len(article.content.encode('utf-8')) * BASE_PRICE
    if not paywall.check_payment():
        return paywall.preview(article.preview_dict)
    return article.content



@app.route('/compute/<computations>')
def get_expensive_stuff(computations):
    # here we could observe the request and calculate the amount to pay based on request data
    computations = int(computations)
    # this is the base amount!
    paywall.amount += 0.0001

    # now we also add dynamic pricing based on the request param!
    paywall.amount += 0.000001 * computations

    # NOTE: since there is no strict association between a specific request
    # (within a certain user session), the amount should always be deterministic
    # for a specific combination of endpoint/request parameters!
    # Otherwise the user will make a request, pay the required amount,
    # When upon repeating the exact same request, only with an added X-Raiden-Payment-Id
    # the amount increases, the resource will not be unlocked!

    # We want to be able to have control over when the paywall is checked.
    if not paywall.check_payment():
        # return paywall.preview(None)
        return paywall.preview(f'If you pay, this would compute {computations} rounds of computations!')
    # Because then we could price heavy computation, before 
    # actually having to do the compuation
    for _ in range(computations):
        pr = 213123
        pr * pr
        pr = pr + 1
    return f"Thank you for paying! Here is the result of your computation: {pr}"
