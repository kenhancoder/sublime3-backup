import os
import sublime_plugin


class TerminalViewExec(sublime_plugin.WindowCommand):

    _init_args = {}

    def run(self, **kwargs):
        # Get the title for the view.
        name = kwargs.get("name", "Executable")

        # Custom environment variables are ignored for now. LinuxPty should be
        # able to handle that in the future.
        env = kwargs.get("env", {})
        env = os.environ.copy().update(env)

        # Get the command that we'll invoke.
        cmd = kwargs.get("cmd", [])
        if not cmd:
            cmd = [kwargs.get("shell_cmd", "")]
        
        # Get the cwd.
        working_dir = kwargs.get("working_dir")
        if not working_dir:
            view = self.window.active_view()
            if view and view.file_name():
                working_dir = os.path.basedir(view.file_name())
            else:
                working_dir = env.get("HOME", "")
                if not working_dir:
                    working_dir = "/"
        
        # If there's init args, get those.
        args = kwargs.get("args", "")
        invocation = " ".join(cmd)
        if not args:
            # Otherwise, prompt the user for init args.
            self.name = name
            self.invocation = invocation
            self.working_dir = working_dir
            # Retrieve the init args for lazy people
            cached_args = self.__class__._init_args.get(invocation, "")
            title = 'Arguments for "{}" '.format(invocation)
            if cached_args:
                title += ":"
            else:
                title += "(press Enter for no args): "
            self.window.show_input_panel(title,
                                         cached_args,
                                         self._on_done,
                                         None,
                                         None)
        else:
            self._run(invocation, working_dir, name)

    def _on_done(self, text):
        # Cache the init args for lazy people
        self.__class__._init_args[self.invocation] = text
        self.invocation += " " + text
        self._run(self.invocation, self.working_dir, self.name)

    def _run(self, cmd, cwd, title):
        self.window.run_command("terminal_view_open",
                                {
                                    "cmd": cmd,
                                    "cwd": cwd,
                                    "title": title,
                                    "keep_open": True
                                })
