from quantumlounge.content.base import Content

def test_create(cstore):
    f = Content()
    i = cstore.put(f)
    assert len(str(i))==24

def test_get(cstore):
    f = Content(_parent_id="foobar")
    i = cstore.put(f)
    f2 = cstore[i]
    assert f2._parent_id == "foobar"

def test_parent_chain(cstore):
    f1 = Content()
    i1 = cstore.put(f1)
    f1 = cstore[i1]

    # create a subfolder
    f2 = Content()
    f2._parent=f1
    i2 = cstore.put(f2)

    f2 = cstore[i2]
    assert f2._parent is not None
    p = f2._parent
    assert p._id == f1._id

    assert f1._parent is None
    assert f1._parent_id is None

def test_get_recursive_children_ids(cstore):
    """try to obtain the ids of the nodes in the subtree of a Content"""

    # create highest level
    main = cstore[cstore.put(Content(title="main"))]

    # create 5 nodes on level 1 beneath
    n=0
    for i in range(1,5):
        f1 = cstore[cstore.put(Content(_id="l-%s" %i, _parent_id=main.oid))]
        n=n+1
        for j in range(1,5):
            f2 = cstore[cstore.put(Content(_id="l-%s-%s" %(i,j), _parent_id=f1.oid))]
            n=n+1

    assert len(main.subtree_ids) == n

    # check one inbetween
    f = cstore['l-1']
    assert len(f.subtree_ids)==4

def test_ancestors_delete_leaf(cstore):

    main = cstore[cstore.put(Content(_id='root',title="main"))]
    for i in range(1,5):
        f1 = cstore[cstore.put(Content(_id="l-%s" %i, title="level1-%s" %i, _parent_id=main.oid))]
        for j in range(1,5):
            f2 = cstore[cstore.put(Content(_id="l-%s-%s" %(i,j), title="level1-%s-%s" %(i,j), _parent_id=f1.oid))]

    # delete a leaf node
    f = cstore['l-1-2']
    assert f._ancestors==['root','l-1']
    f._parent = None
    cstore.update(f)
    assert f._ancestors==[]

    # check ancestors
    f = cstore['l-1']
    assert len(f.subtree_ids)==3


def test_ancestors_delete_middle(cstore):

    main = cstore[cstore.put(Content(_id='root'))]
    for i in range(1,5):
        f1 = cstore[cstore.put(Content(_id="l-%s" %i, _parent_id=main.oid))]
        for j in range(1,5):
            f2 = cstore[cstore.put(Content(_id="l-%s-%s" %(i,j), _parent_id=f1.oid))]

    # delete a node inbetween
    f = cstore['l-1']
    f._parent = None
    cstore.update(f)
    assert f._ancestors==[]

    # check ancestors
    f = cstore['l-1-2']
    assert f._ancestors==['l-1']


def test_ancestors_reroot(cstore):

    main = cstore[cstore.put(Content(_id='root',title="main"))]
    main2 = cstore[cstore.put(Content(_id='root2',title="main"))]
    for i in range(1,5):
        f1 = cstore[cstore.put(Content(_id="l-%s" %i, title="level1-%s" %i, _parent_id=main.oid))]
        for j in range(1,5):
            f2 = cstore[cstore.put(Content(_id="l-%s-%s" %(i,j), title="level1-%s-%s" %(i,j), _parent_id=f1.oid))]

    # delete a node inbetween
    f = cstore['l-1']
    f._parent = main2
    cstore.update(f)
    assert f._ancestors==['root2']

    # check ancestors
    f = cstore['l-1-2']
    assert f._ancestors==['root2','l-1']



