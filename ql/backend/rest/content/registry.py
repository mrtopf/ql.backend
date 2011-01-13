import common
import poll
import reprs

r_common = {
        'subtree' : common.SubTree,
        'query' : common.Query,
        'parents' : common.Parents,
        'children' : common.Children,
        'default' : common.Default,
}

r_poll = {
        'vote' : poll.Vote,
        'voted' : poll.Voted,
        'results' : poll.Results,
}
r_poll.update(r_common)

type_registry = {
    'status' : r_common,
    'link' : r_common,
    'folder' : r_common,
    'poll' : r_poll,
     
}

###
### representations
###

fmt_registry = {
        'json' : reprs.Representation,
        'html' : reprs.GenericHTML
}

__all__ = ['type_registry', 'fmt_registry']
