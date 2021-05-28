import { Button } from "@material-ui/core";
import { Story } from "@storybook/react";
import React from "react";
import { AlertServiceProvider, useAlert } from "../AlertServiceProvider";

export default {
  title: "AlertServiceProvider",
  component: AlertServiceProvider,
};

const View = ({ traceback }: { traceback?: string }): React.ReactElement => {
  const alertDialog = useAlert();

  const handleClick = async () => {
    await alertDialog({
      title: "Something went wrong",
      description:
        "Proin efficitur venenatis elit rhoncus venenatis. Nam molestie urna quis dolor lobortis accumsan. Suspendisse viverra urna non nisl egestas rutrum.",
      traceback: traceback,
    });
  };

  return <Button onClick={handleClick}>Open Alert Dialog</Button>;
};

const Template: Story = ({ traceback }: { traceback?: string }) => {
  return (
    <AlertServiceProvider>
      <View traceback={traceback} />
    </AlertServiceProvider>
  );
};

export const Default = Template.bind({});
export const WithTraceback = Template.bind({});
WithTraceback.args = {
  traceback:
    'Traceback (most recent call last):\n  File "/Users/luiz/projects/mariner/.venv/lib/python3.8/site-packages/flask/app.py", line 1950, in full_dispatch_request\n    rv = self.dispatch_request()\n  File "/Users/luiz/projects/mariner/.venv/lib/python3.8/site-packages/flask/app.py", line 1936, in dispatch_request\n    return self.view_functions[rule.endpoint](**req.view_args)\n  File "/Users/luiz/projects/mariner/mariner/server/api.py", line 201, in printer_command\n    printer.stop_printing()\n  File "/usr/local/opt/python@3.8/Frameworks/Python.framework/Versions/3.8/lib/python3.8/unittest/mock.py", line 1081, in __call__\n    return self._mock_call(*args, **kwargs)\n  File "/usr/local/opt/python@3.8/Frameworks/Python.framework/Versions/3.8/lib/python3.8/unittest/mock.py", line 1085, in _mock_call\n    return self._execute_mock_call(*args, **kwargs)\n  File "/usr/local/opt/python@3.8/Frameworks/Python.framework/Versions/3.8/lib/python3.8/unittest/mock.py", line 1140, in _execute_mock_call\n    raise effect\nmariner.exceptions.UnexpectedPrinterResponse: foobar\r\n\n',
};
