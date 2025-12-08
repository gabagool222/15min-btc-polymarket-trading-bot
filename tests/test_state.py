from src.state import TradeState


def test_pair_cost_and_locked_profit():
    st = TradeState()
    st.update_after_fill("YES", price=0.4, qty=100)
    st.update_after_fill("NO", price=0.5, qty=100)
    pair_cost, avg_yes, avg_no = st.pair_cost()
    assert round(avg_yes, 3) == 0.4
    assert round(avg_no, 3) == 0.5
    assert round(pair_cost, 3) == 0.9
    assert st.locked_profit() > 0
