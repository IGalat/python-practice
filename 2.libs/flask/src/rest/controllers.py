from rest.article_controller import article_controller
from rest.comment_controller import comment_controller

rest_controllers = {
    "/articles": article_controller,
    "/comments": comment_controller,
}
