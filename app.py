import streamlit as st
from agent.react_agent import ReactAgent
from file_history_store import filehistory_store

#标题
st.title("React Agent")
st.divider()

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "file_history_store" not in st.session_state:
    st.session_state["file_history_store"] = filehistory_store()    

if "message" not in st.session_state:   #创建历史记录列表
    st.session_state["message"] = st.session_state["file_history_store"].get_history()
    
for item in st.session_state["message"]:
    st.chat_message(item["role"]).write(item["content"])
    
#用户输入提示词
prompt = st.chat_input("请输入您的问题：")
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})
    
    with st.spinner("智能客服思考中"):
        res=st.session_state["agent"].execute_stream(prompt,st.session_state["message"])   #res是一个迭代器，传入历史消息使Agent记住上下文
        cache_list=[]
        def  capture(gengrator,cache_list=cache_list):        #捕获迭代器中的数据存入列表中，因为迭代器输出一个字紧接着输出下一个字，上一个字就没了
            for item in gengrator:
                cache_list.append(item)
                yield item                         #原样返回迭代器
                
        st.chat_message("assistant").write_stream(capture(res))
        st.session_state["message"].append({"role": "assistant", "content": cache_list[-1]})
        st.session_state["file_history_store"].add_history(st.session_state["message"])