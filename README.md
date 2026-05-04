
# AGIS Core

**Adaptive Geometric Intelligence System**

A real-time uncertainty-to-action engine using statistical geometry.

## 🎯 What It Does

AGIS converts streaming data instability into geometric representations, then transforms those geometries into actionable decisions.

**Pipeline:**

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run API server
uvicorn api.main:app --reload

# Test it
curl http://localhost:8000/action
```

## 📡 API Endpoints

- `GET /` - System info
- `POST /ingest` - Add data point
- `GET /state` - Current statistical state
- `GET /geometry` - Geometric analysis
- `GET /drift` - Drift detection metrics
- `GET /action` - Recommended action
- `GET /simulate/{n}` - Run simulation

##  Core Concepts

### 1. **Statistical Encoding**
Raw data → uncertainty space representation
- Mean, variance, entropy
- Trend detection
- Confidence scoring

### 2. **Geometric Approximation**
States → manifold structure
- Curvature (rate of uncertainty change)
- Gradient flow (direction of change)
- Instability zones

### 3. **Drift Detection**
Monitors distribution shifts
- KL divergence
- Statistical tests
- Adaptive thresholds

### 4. **Action Engine**
Geometry → Decisions
- **Stabilize**: High drift → reduce risk
- **Explore**: Low drift + positive trend → increase exposure
- **Hold**: Flat geometry → maintain position
- **Caution**: High curvature → monitor closely

## 📊 Architecture

## 🔬 Testing

```bash
python tests/test_geometry.py
```

##  License

MIT License - see LICENSE file

---

**Status**: MVP - Working prototype
**Version**: 0.1.0
