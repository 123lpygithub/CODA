#include "user_scripts_dispatcher.h"

#include <stddef.h>

#include <algorithm>
#include <memory>
#include <utility>

#include "content/public/renderer/render_thread.h"
#include "extension_frame_helper.h"

namespace user_scripts {

// ex ChromeExtensionsDispatcherDelegate
UserScriptsDispatcher::UserScriptsDispatcher()
    : user_script_set_manager_observer_(this) {
    //: delegate_(std::move(delegate))
    //,
    //  content_watcher_(new ContentWatcher()),
    //  source_map_(&ui::ResourceBundle::GetSharedInstance()),
    //  v8_schema_registry_(new V8SchemaRegistry),
    //activity_logging_enabled_(false) 
      user_script_set_manager_.reset(new UserScriptSetManager());
      script_injection_manager_.reset(
          new ScriptInjectionManager(user_script_set_manager_.get()));
      user_script_set_manager_observer_.Add(user_script_set_manager_.get());
}

UserScriptsDispatcher::~UserScriptsDispatcher() {
}

void UserScriptsDispatcher::OnRenderThreadStarted(content::RenderThread* thread) {
  //thread->RegisterExtension(extensions::SafeBuiltins::CreateV8Extension());
}

void UserScriptsDispatcher::OnUserScriptsUpdated(const std::set<HostID>& changed_hosts) {
  //UpdateActiveExtensions();
}

void UserScriptsDispatcher::OnRenderFrameCreated(content::RenderFrame* render_frame) {
  script_injection_manager_->OnRenderFrameCreated(render_frame);
  //content_watcher_->OnRenderFrameCreated(render_frame);
}

//void Dispatcher::OnSetActivityLoggingEnabled(bool enabled) {
//  activity_logging_enabled_ = enabled;
//  if (enabled) {
//    for (const std::string& id : active_extension_ids_)
//      DOMActivityLogger::AttachToWorld(DOMActivityLogger::kMainWorldId, id);
//  }
//  script_injection_manager_->set_activity_logging_enabled(enabled);
//  user_script_set_manager_->set_activity_logging_enabled(enabled);
//}

//void Dispatcher::UpdateActiveExtensions() {
//  std::set<std::string> active_extensions = active_extension_ids_;
//  user_script_set_manager_->GetAllActiveExtensionIds(&active_extensions);
//  delegate_->OnActiveExtensionsUpdated(active_extensions);
//}

}