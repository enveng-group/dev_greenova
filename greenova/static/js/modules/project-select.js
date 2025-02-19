export class ProjectSelect {
    constructor() {
document.addEventListener('htmx:configRequest', (event) => {
    const select = event.detail.elt;
    if (select.id === 'project-select') {
        const projectId = select.value;
        if (projectId) {
            event.detail.path = `/projects/${projectId}/content/`;
        }
    }
});
    }


}