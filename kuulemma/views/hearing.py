from flask import Blueprint, redirect, render_template, url_for

from ..models import Hearing

hearing = Blueprint(
    name='hearing',
    import_name=__name__,
    url_prefix='/kuulemiset'
)


# Redirects to the first hearing before the real index page is implemented.
@hearing.route('')
def index():
    hearing = Hearing.query.first()
    if not hearing:
        return redirect(url_for('frontpage.index'))

    return redirect(url_for(
        'hearing.show',
        hearing_id=hearing.id,
        slug=hearing.slug
    ))


@hearing.route('/<int:hearing_id>-<slug>')
def show(hearing_id, slug):
    hearing = Hearing.query.get_or_404(hearing_id)

    if hearing.slug != slug:
        return redirect(
            url_for('hearing.show', hearing_id=hearing_id, slug=hearing.slug)
        )

    commentable_sections_string = hearing.get_commentable_sections_string()

    return render_template(
        'hearing/show.html',
        hearing=hearing,
        commentable_sections_string=commentable_sections_string,
        hearing_page_active=True
    )
