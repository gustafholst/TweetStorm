from django import template

register = template.Library()

@register.simple_tag(name='get_vote')
def get_users_vote(post, user) -> int:
    vote = post.vote_set.filter(voter=user).first()
    if vote:
        return vote.vote
    return 0
