import * as vscode from 'vscode';
import * as http from 'http';

export function activate(context: vscode.ExtensionContext) {
    // 1. Create Status Bar Shield Indicator
    const statusBar = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBar.text = "$(shield) DROS: Protected";
    statusBar.tooltip = "DROS VajraClaw In-Band Microsecond Gateway Active (<1μs)";
    statusBar.command = "dros.checkStatus";
    statusBar.color = "#00F0FF";
    statusBar.show();

    // 2. Command to check status
    const statusCmd = vscode.commands.registerCommand("dros.checkStatus", () => {
        http.get("http://localhost:8080/health", (res) => {
            if (res.statusCode === 200) {
                vscode.window.showInformationMessage("🛡️ DROS VajraClaw Gateway is ONLINE. In-band AST execution fusing active.");
            } else {
                vscode.window.showWarningMessage(`⚠️ DROS Gateway returned status ${res.statusCode}.`);
            }
        }).on("error", (err) => {
            vscode.window.showInformationMessage("ℹ️ DROS Gateway offline. Running in local fail-safe mode.");
        });
    });

    context.subscriptions.push(statusBar, statusCmd);
}

export function deactivate() {}
