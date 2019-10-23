from apps import app
app.config['TEMPLATES_AUTO_RELOAD']=True

@app.template_filter('gender')
def gender(value):
    if value==1:
        return "男"

    return "女"