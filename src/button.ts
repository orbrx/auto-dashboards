/*
 * Copyright 2017-2023 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { CommandToolbarButton } from '@jupyterlab/apputils';
import { DocumentRegistry, DocumentWidget } from '@jupyterlab/docregistry';
import { CommandRegistry } from '@lumino/commands';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { isNotebook } from './utils';

import { CommandIDs } from './utils';

export class StreamlitButtonExtension
  implements
    DocumentRegistry.IWidgetExtension<DocumentWidget, DocumentRegistry.IModel>
{
  commands: CommandRegistry;
  constructor(commands: CommandRegistry) {
    this.commands = commands;
  }
  createNew(widget: DocumentWidget): IDisposable {
    let button: CommandToolbarButton | undefined;

    if (isNotebook(widget.context.path)) {
      button = new CommandToolbarButton({
        commands: this.commands,
        id: CommandIDs.translate,
        label: ''
      });
    } else {
      button = new CommandToolbarButton({
        commands: this.commands,
        id: CommandIDs.openFromEditor,
        label: ''
      });
    }
    widget.toolbar.insertItem(99, 'streamlit', button);
    return new DisposableDelegate(() => {
      button?.dispose();
    });
  }
}
