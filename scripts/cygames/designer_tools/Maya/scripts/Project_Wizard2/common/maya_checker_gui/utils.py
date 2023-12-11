import maya.cmds as cmds
import webbrowser

def create_progress_bar(max_count: int) -> any:
    """プログレスバーを作成

    Args:
        max_count (int): プログレスバーのmax step

    Returns:
        any: プログレスバー
    """
    # プログレスバーの作成
    progress_window = cmds.window(title="Progress", widthHeight=(300, 50))
    cmds.columnLayout(adjustableColumn=True)
    progress_bar = cmds.progressBar(maxValue=max_count, width=300)
    cmds.showWindow(progress_window)
    return progress_window, progress_bar

def search_website(url, search_query):
    search_url = f"{url}#:~:text={search_query}"
    webbrowser.open(search_url)