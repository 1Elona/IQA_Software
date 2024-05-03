from graphviz import Digraph


def draw_er_diagram():
    # 创建 Digraph 对象
    dot = Digraph(comment='The ER Diagram')

    # 添加实体
    dot.node('Task', 'Task', shape='rectangle')
    dot.node('SubTask', 'SubTask', shape='rectangle')
    dot.node('User', 'User', shape='rectangle')

    # 添加实体属性
    dot.node('TaskId', 'Id (PK)', shape='ellipse')
    dot.node('TaskName', 'task_name', shape='ellipse')
    dot.node('TaskProgress', 'progress', shape='ellipse')
    # 更多的 Task 属性...
    dot.node('TaskInput', 'input', shape='ellipse')
    dot.node('TaskOutput', 'output', shape='ellipse')
    dot.node('TaskStatus', 'status', shape='ellipse')
    dot.node('TaskCreateTime', 'create_time', shape='ellipse')
    dot.node('TaskMode', 'mode', shape='ellipse')
    dot.node('TaskDescribe', 'describe', shape='ellipse')
    dot.node('TaskReferFolder', 'refer_folder', shape='ellipse')
    dot.node('TaskUsername', 'username', shape='ellipse')
    dot.node('TaskUUID', 'uuid', shape='ellipse')

    # 更多的 SubTask 属性...
    dot.node('SubTaskId', 'Subid (PK)', shape='ellipse')
    dot.node('SubTaskName', 'Taskname', shape='ellipse')
    dot.node('SubExecuteTime', 'Execute_Time', shape='ellipse')
    # ...

    # User属性
    dot.node('UserId', 'id (PK, Auto)', shape='ellipse')
    dot.node('UserUsername', 'username', shape='ellipse')
    dot.node('UserPassword', 'password', shape='ellipse')
    dot.node('UserYhsf', 'yhsf', shape='ellipse')

    # 添加表示实体关系的菱形
    dot.node('relUserTask', '', shape='diamond')
    dot.node('relTaskSubTask', '', shape='diamond')

    # 连接实体和关系
    dot.edge('User', 'relUserTask')
    dot.edge('relUserTask', 'Task')

    dot.edge('Task', 'relTaskSubTask')
    dot.edge('relTaskSubTask', 'SubTask')

    # 连接实体和属性
    # Task实体与属性连接
    dot.edges([('Task', 'TaskId'), ('Task', 'TaskName'), ('Task', 'TaskProgress'), ('Task', 'TaskInput'),
               ('Task', 'TaskOutput'), ('Task', 'TaskStatus'), ('Task', 'TaskCreateTime'), ('Task', 'TaskMode'),
               ('Task', 'TaskDescribe'), ('Task', 'TaskReferFolder'), ('Task', 'TaskUsername'), ('Task', 'TaskUUID')])
    # SubTask实体与属性连接
    dot.edges([('SubTask', 'SubTaskId'), ('SubTask', 'SubTaskName'), ('SubTask', 'SubExecuteTime')])
    # User实体与属性连接
    dot.edges([('User', 'UserId'), ('User', 'UserUsername'), ('User', 'UserPassword'), ('User', 'UserYhsf')])

    # 打印生成的源代码
    print(dot.source)

    # 保存和渲染图形
    dot.render('er_diagram', format='png', view=True)


if __name__ == '__main__':
    draw_er_diagram()